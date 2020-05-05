from utils import *

tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.INFO)

MODEL_VERSION = "002"
GRAPH_DIR = "graphs"
MODEL_NAME = "StarGAN"
EXPORT_DIR_BASE = "optimized_saved_model"


def build_saved_model():
    graph_file_path = os.path.join(GRAPH_DIR, "{}_v{}".format(MODEL_NAME, MODEL_VERSION))
    export_path = os.path.join(EXPORT_DIR_BASE, MODEL_VERSION)

    builder = tf.saved_model.builder.SavedModelBuilder(export_path)

    with tf.gfile.GFile(graph_file_path, 'rb') as pf:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(pf.read())

    [input_bytes, target_domain_label, output_bytes] \
        = tf.import_graph_def(graph_def,
                              name="",
                              return_elements=["input_bytes:0",
                                               "target_domain_label:0",
                                               "output_bytes:0"])

    with tf.Session(graph=output_bytes.graph) as sess:
        input_bytes_info = tf.compat.v1.saved_model.utils.build_tensor_info(input_bytes)
        target_domain_label_info = tf.compat.v1.saved_model.utils.build_tensor_info(target_domain_label)
        output_bytes_info = tf.compat.v1.saved_model.utils.build_tensor_info(output_bytes)

        signature_definition = tf.saved_model.signature_def_utils.build_signature_def(
            inputs={
                "input_bytes": input_bytes_info,
                "target_domain_label": target_domain_label_info,
            },
            outputs={
                "output_bytes": output_bytes_info
            },
            method_name=tf.saved_model.signature_constants.PREDICT_METHOD_NAME
        )

        builder.add_meta_graph_and_variables(
            sess,
            [tf.saved_model.tag_constants.SERVING],
            signature_def_map={
                tf.saved_model.signature_constants.DEFAULT_SERVING_SIGNATURE_DEF_KEY:
                    signature_definition
            }
        )

    builder.save()


def main():
    build_saved_model()
    print(' [*] Model has saved!')


if __name__ == '__main__':
    main()
